
const fileSys = require("fs-extra");
const path = require("path");
const Yaml = require("js-yaml");
const logs = require("../logUtils");
const prompt = require("prompt-sync")({ sigint: true });
const crypto = require("crypto");
const RippleAPI = require("ripple-lib").RippleAPI;
const { create, globSource } = require("ipfs-core");
const xAddr = require("xrpl-tagged-address-codec");
const Hash = require("ipfs-only-hash");
const figlet = require("figlet");
const colorize = require("json-colorizer");

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

let config;
try {
  config = Yaml.load(fileSys.readFileSync("./setup.yml", "utf8"));
} catch (error) {
  console.log(`Error in index.js: ${error}`);
  process.exit(-1);
}

const xAPI = new RippleAPI({ server: config.xrp.network });

let iAPI;
let epochCreateTime = Date.now();

class Ledger {
	constructor() {
    
	}


  // Write meta.json
  async WriteMetaData(configSettings) {
    try {
      let metaFile = configSettings.buildDestFolder + path.sep + "meta.json";
      logs.info(`writting data to meta file: ${metaFile}`);
      fileSys.writeFileSync(
        metaFile,
        JSON.stringify(configSettings.meta, null, 4)
      );
    } catch (error) {
      CatchError(error);
    }
  }
  
  // Fetch nft-content files cids, returns cids for nft content files, gathers SHA256 for each file
  async  GetNFTFileHashes(contentDirectory) {
    try {
      logs.info(`gathering IPFS CID & SHA256 hashes to add to meta data file...`);
      //options specific to globSource
      const globSourceOptions = { recursive: true };
  
      let cids = [];
      let excludeHead = path.sep + contentDirectory.split(path.sep).pop();
      excludeHead = excludeHead.replace(/\//g, "").replace(/\\/g, "");
  
      for await (let value of globSource(contentDirectory, globSourceOptions)) {
        if (!value.path.endsWith(excludeHead)) {
          let fileData = await fileSys.readFileSync(value.content.path);
          const cid = await Hash.of(fileData);
          const hash = crypto.createHash("sha256");
          hash.update(fileData);
          const hdigest = hash.digest("hex");
          cids.push({ file: value.path, cid: cid, sha256: hdigest });
          logs.info(
            `adding '${value.path}' with cid hash '${hdigest}' to meta data...`
          );
        }
      }
      return cids;
    } catch (error) {
      CatchError(error);
    }
  }
  
  // Update xrp wallet data
  async updateXRPWalletData(walletData, walletAddress, xAPI) {
    try {
      //Get some account info
      // - Fee calculation
      let fee = await xAPI.getFee();
      fee = (parseFloat(fee) * 1000000).toFixed(0) + "";
      // Seq calculation
      let accInfo = await xAPI.getAccountInfo(walletAddress.address);
      let seqNum = accInfo.sequence;
  
      // TX Template for update
      let tempWalletData = {
        TransactionType: "AccountSet",
        Account: walletAddress.address,
        Fee: fee,
        Sequence: seqNum,
        SetFlag: 5,
      };
  
      //Merge options with template
      let txWallet = { ...tempWalletData, ...walletData };
  
      //Prepare TX for sending to ledger
      let txJSON = JSON.stringify(txWallet);
      let signedTX = xAPI.sign(txJSON, walletAddress.secret);
  
      //Submit the signed transaction to the ledger (need to add validation here)
      await xAPI
        .submit(signedTX.signedTransaction)
        .then(function (tx) {
          logs.debug(`attempting submition of transaction: ${txJSON}`);
          logs.debug(`tentative message: ${tx.resultMessage}`);
          logs.info(
            `tx status code: ${tx.resultCode} , tx hash ${tx.tx_json.hash}`
          );
        })
        .catch(function (e) {
          logs.warn(`tran failure to send data: ${e}`);
        });
    } catch (error) {
      CatchError(error);
    }
  }
  
  async  GetBuildConfig(dataDir) {
    try {
      //options specific to globSource
      const globSourceOptions = { recursive: true };
      let workOptions = [];
      //look for all build directories
      for await (const file of globSource(dataDir + path.sep + "input", globSourceOptions)) {
        let pathCount = file.path.split("/").length - 1;
        if (pathCount < 3 && pathCount > 1) {
          file.path = __dirname + file.path;
          //Deal w/ Windows
          if (process.platform === "win32") {
            file.path = file.path.replace(/\//g, "\\");
          }
          workOptions.push(file);
        }
      }
      //sanity check
      if (!workOptions) {
        throw Error(
          "no valid build directories found in input directory, exiting"
        );
      }
      
      //currently hardcoded
      let buildDir = {
        buildSourceFolder: dataDir + path.sep + "input" + path.sep + "Example",
      };
  
      logs.info(buildDir);
  
      // Get the make.yml settings for use during the build
      let buildConfigPath = buildDir.buildSourceFolder + path.sep + "make.yml";
      let buildConfig = await Yaml.load(
        fileSys.readFileSync(buildConfigPath, "utf8")
      );
  
      //Calculate the destination build directory
      let destName =
        buildDir.buildSourceFolder
          .split(path.sep)
          .pop()
          .toLowerCase()
          .replace(/\s/g, "") + `${epochCreateTime}`;
      let buildDestFolder = dataDir + path.sep + "output" + path.sep + destName;
  
      //Return the results
      return {
        ...buildConfig.settings,
        ...{
          buildSourceFolder: buildDir.buildSourceFolder,
          buildDestFolder: buildDestFolder,
        },
      };
    } catch (error) {
      CatchError(error);
    }
  }
  
  // Get or Create XRP Address
  // - convert this to inquire later...
  async GetXRPWalletAddress() {
    try {
      let address = {};
      let secret = "ss71fBzFpSXMixT6ZBoXNgkFeBo9y";
      let validAcc = false;
  
      let tempAddr = await xAPI.deriveKeypair(secret);
      address.address = await xAPI.deriveAddress(tempAddr.publicKey);
      address.xAddress = await xAddr.Encode({ account: address.address });
      address.secret = secret;
      logs.info(`account secret appears valid: '${secret}'`);
      validAcc = true;
  
      return address;
    } catch (error) {
      CatchError(error);
    }
  }
  
  // Build Domain Field Pointer information
  async BuildDomainPointer(resources) {
    /* 
        Example
  
        @xnft:
        btih:1e3ec2d9d231b7dbe0b0ba2db911cb97eadd40bb
        ipfs:Qmct4KDxLbpXTgpKPXYv6enj4yRBCNkxtfAEWP9jFqLtkW
        ilpd:$ilp.uphold.com/ZQ9a44qFAxLk
        http:nft.xrpfs.com
        
        157 bytes of 256 MAX
  
        OR
  
        @xnft:meta.json
        btih:1e3ec2d9d231b7dbe0b0ba2db911cb97eadd40bb
        ipfs:Qmct4KDxLbpXTgpKPXYv6enj4yRBCNkxtfAEWP9jFqLtkW
        ilpd:$ilp.uphold.com/ZQ9a44qFAxLk
        http:nft.xrpfs.com
        
        166 bytes of 256 MAX
  
        -------------------------------------------------------------------------------------------------------------
  
        @[xnft]: <- Defines this group of resources is a XRP NFT resource group | meta.json <- additional data (opt.)
        [btih]:[Torrent Hash Address]
        [ipfs]:[IPFS Data]
        [ilpd]:[Dynamic ILP pointer, overrides defined meta pointer data]
        [http]:[Domain hosting data (base url)]
  
        [service identification]::
        [protocal]:[resource address / instruction] (pointers)
  
        Must be less then 256 Chars / bytes
        NewLine sep
  
        resources -> k/v Obj {"protocol" : "resource address / instruction", "protocol" : "resource address / instruction", ...}
        Max 256 data, will fail if over!
  
    */
    try {
      //Build the domain value out
      let domainValue = "";
      domainValue += "@xnft:\n";
      //Add the protos and resources
      // - Add size validation here, add as much as possible, then warn on failed additions / rev2
      Object.entries(resources).forEach(([key, value]) => {
        domainValue += `${key}:${value}\n`;
      });
  
      //Validate the size of the output does not exceed byte limit
      let bufSize = Buffer.from(domainValue).length;
      if (bufSize > 256) {
        throw Error(`Domain value exceeds max value of 256, ${bufSize}`);
      }
      //Some Logging
      logs.info(
        `Domain value: \n${domainValue}Value size: ${bufSize} of 256 bytes used`
      );
  
      //Convert for use in Domain Account set
      let hexDomValue = new Buffer.from(domainValue)
        .toString("hex")
        .toUpperCase();
      logs.info(`Domain value in hex: ${hexDomValue}`);
      return hexDomValue;
    } catch (error) {
      CatchError(error);
    }
  }
}

  module.exports = new Ledger()