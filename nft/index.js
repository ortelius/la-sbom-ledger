const dotenv = require('dotenv')
const path = require('path')
const util = require('util')
const ipfsStorage = require('./IPFSStorage')
const xrpledger = require('./XRPLedger')

dotenv.config()

async function main() {
	try {

		const pathToFile = path.resolve(__dirname, 'example.json')

		const { cid } = await ipfsStorage.upload(pathToFile)

		const { ipfsUrl } = await ipfsStorage.retrieve(cid)

		console.log(`ipsUrl: ${ipfsUrl}`)

		const mintTokenTransactionResult = await xrpledger.mintToken(ipfsUrl)

		console.log(
			'mintTokenTransactionResult:',
			util.inspect(mintTokenTransactionResult)
		)

		const tokens = await xrpledger.getTokens()

		console.log('Tokens:', util.inspect(tokens.result.account_nfts))
	} catch (error) {
		console.log(error.stack)
		console.log(error)
		console.log(`error: ${error.message}`)
	}
}

main()
