`use strict`;

const fileSys = require("fs-extra");
const path = require("path");
const Yaml = require("js-yaml");
const logs = require("./logUtils");
const prompt = require("prompt-sync")({ sigint: true });
const crypto = require("crypto");
const RippleAPI = require("ripple-lib").RippleAPI;
const { create, globSource } = require("ipfs-core");
const xAddr = require("xrpl-tagged-address-codec");
const Hash = require("ipfs-only-hash");
const figlet = require("figlet");
const colorize = require("json-colorizer");
const ipfsStorage = require('./nft/IPFSStorage')
const Ledger = require("./sbom-ledger/Ledger");


// get configuration
let config;
try {
  config = Yaml.load(fileSys.readFileSync("setup.yml", "utf8"));
} catch (error) {
  console.log(`Error in index.js: ${error}`);
  process.exit(-1);
}

// Global intantiation
const xAPI = new RippleAPI({ server: config.xrp.network });
let epochCreateTime = Date.now();

// catch and display the errors nicely
function CatchError(err) {
  if (typeof err === "object") {
    if (err.message) {
      logs.error(err.message);
    }
    if (err.stack) {
      logs.error("StackTrace:");
      logs.error(err.stack);
    }
  } else {
    logs.error("error in CatchError:: argument is not an object");
  }
  prompt("something went wrong, press Enter to exit script...");
  process.exit();
}

//Main execution block for script
async function main() {
  try {
    process.stdout.write("\033c");
    let output = figlet.textSync("Ortelius", {
      font: "Small",
      horizontalLayout: "default",
      verticalLayout: "default",
      width: 120,
      whitespaceBreak: false,
    });
    console.log(output);

    // Init IPFS
    logs.info("starting IPFS node for content distribution");

    // - Testing, seems updated IPFS package has some bugs
    // iAPI = await create({
    //   repo: config.ipfs.node,
    // });

    // Choose the build path to use and get the build config    
    let dataDir = __dirname + path.sep + "data";         
    let buildSettings = await Ledger.GetBuildConfig(dataDir);

    //Confirm the settings being used for this build with a confirmation
    console.log(colorize(JSON.stringify(buildSettings, null, 2)));
    logs.info(
      `user validated build settings for ${buildSettings.buildDestFolder}`
    );

    //Create the build folder and copy the NFT contents for building
    !fileSys.existsSync(buildSettings.buildDestFolder) &&
      fileSys.mkdirSync(buildSettings.buildDestFolder);
    logs.info(`created build destination: '${buildSettings.buildDestFolder}'`);
    logs.info(
      `copying date from source '${
        buildSettings.buildSourceFolder + path.sep + buildSettings.contentFolder
      }' to '${buildSettings.buildDestFolder}'`
    );
    await fileSys.copy(
      buildSettings.buildSourceFolder + path.sep + buildSettings.contentFolder,
      buildSettings.buildDestFolder
    );

    logs.info();

    // Get additional meta of nft content folder
    // - Content IDentifiers for IPFS and SHA256 values for files
    buildSettings.meta.hashes = await Ledger.GetNFTFileHashes(
      buildSettings.buildDestFolder
    );

    // Starts the XRP Ledger API interface
    logs.info(
      `Init connection to xrp ledger: ${JSON.stringify(
        config.xrp.network,
        null,
        4
      )}`
    );
    await xAPI.connect();

    // Generate NFT wallet address to be funded by author address
    let address = await Ledger.GetXRPWalletAddress();

    // Display the account for the user
    logs.info(`NFT Wallet Address: (Classic)  '${address.address}'`);
    logs.info();

    // Add the public wallet address to the meta data
    buildSettings.meta.details.NFTWalletAddress = address.address.toString();
    buildSettings.meta.details.NFTWalletXAddress = address.xAddress.toString();

    // - Write Meta data to nft-content folder for IPFS packaging
    buildSettings.meta.created = epochCreateTime;
    buildSettings.meta.framework = "https://github.com/ortelius/ortelius";
    await Ledger.WriteMetaData(buildSettings);

    console.log(colorize(JSON.stringify(buildSettings, null, 2)));
    logs.info(
      `user validated build settings for ${buildSettings.buildDestFolder}`
    );
    logs.info();
    logs.info(buildSettings);
    let cidData = await ipfsStorage.upload(buildSettings.buildSourceFolder + path.sep + "content" + path.sep + "example.json" );

    let baseString = cidData.cid.toString();

    let baseStringURL = `ipfs://${baseString}/`;
    buildSettings.ipfsAddress = baseString;
    logs.info(`(IPFS) content base string recorded as: ${baseStringURL}`);

    logs.info();
    logs.warn(
      `YOU MUST FUND THE NFT ADDRESS w/ 20+ XRP (CLASSIC): '${address.address.toString()}' (XADDRESS): '${address.xAddress.toString()}'`
    );
    // await ValidateFunding(address.address)
    logs.warn(`validation completed, wallet ${address.address} is funded`);

    // - Build the Domain Resource Pointer
    let resources = {};
    // if (btHash) { resources.bith = btHash}
    if (baseString) {
      resources.ipfs = baseString;
    }
    if (buildSettings.meta.webHostingURI) {
      resources.http = buildSettings.meta.webHostingURI;
    }
    if (buildSettings.meta.staticILPAddress) {
      resources.ilpd = buildSettings.meta.staticILPAddress;
    }
    // - Build it
    let xrpDomainField = await Ledger.BuildDomainPointer(resources);
    logs.info(
      `Attempting to set ${address.address} Domain field with resource settings...`
    );
    // Write the data to the NFT Wallet
    await Ledger.updateXRPWalletData({ Domain: xrpDomainField }, address, xAPI);

    logs.info(
      `Validate your NFT data is live (IPFS)(Base Dir): ${baseStringURL}`
    );
    logs.info(
      `Validate your NFT base folder is live: https://gateway.ipfs.io/ipfs/${baseString} `
    );
    logs.info(
      `See your Testnet NFT wallet here: https://testnet.xrpl.org/accounts/${address.address}`
    );
    logs.info();
    
    if (config.system.exitEnabled) {
      logs.warn(
        `Script is set to end in ${config.system.exitScriptTTL} minutes`
      );
      setTimeout(async function () {
        logs.info("Time to close things down...");
        await xAPI.disconnect();
        process.exit();
      }, config.system.exitScriptTTL * 60 * 1000);
    }
  } catch (error) {
    CatchError(error);
    process.exit(-1);
  }
}

main();
