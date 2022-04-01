const dotenv = require('dotenv')
const ipfsStorage = require('./IPFSStorage')

dotenv.config()

async function main() {
	try {
		const { cid } = await ipfsStorage.upload('./example.json')

		const { ipfsUrl } = await ipfsStorage.retrieve(cid)

		console.log(`ipsUrl: ${ipfsUrl}`)
	} catch (error) {
		console.log(`error: ${error.message}`)
	}
}

main()
