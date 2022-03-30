const fs = require('fs')
const { NFTStorage, Blob } = require('nft.storage')
const dotenv = require('dotenv')

dotenv.config()

const endpoint = 'https://api.nft.storage' // the default
const token =
	process.env.NFT_STORAGE_API_TOKEN ||
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk3ODMwMGIzNUMzOEM3NzMxYWNDNjk4NDFiODU4NDNiRmIxRjExN0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY0ODY2MjM1MDcwNiwibmFtZSI6Im9ydGVsaXVzX3Nib21fbGVkZ2VyX2RlbW8ifQ.egQzHqDB83UoK7ynE4fn4dhgIKWLhPP1B9E6qey4KHM' // your API key from https://nft.storage/manage

async function main() {
	const storage = new NFTStorage({ endpoint, token })

	const data = await fs.promises.readFile('example.json')
	const cid = await storage.storeBlob(new Blob([data]))
	console.log({ cid })

	const metadata = {
		name: 'example json',
		description: 'metadata for example json',
		ipfs_url: `https://${cid}.ipfs.nftstorage.link/`
	}

	const status = await storage.status(cid)
	console.log(status)

	// metadata is stored on blockchain
	console.log(metadata)
}

main()
