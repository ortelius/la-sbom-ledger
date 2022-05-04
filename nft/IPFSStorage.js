const fs = require('fs')
const { NFTStorage, Blob } = require('nft.storage')
const token =
	process.env.NFT_STORAGE_API_TOKEN ||
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk3ODMwMGIzNUMzOEM3NzMxYWNDNjk4NDFiODU4NDNiRmIxRjExN0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY0ODY2MjM1MDcwNiwibmFtZSI6Im9ydGVsaXVzX3Nib21fbGVkZ2VyX2RlbW8ifQ.egQzHqDB83UoK7ynE4fn4dhgIKWLhPP1B9E6qey4KHM' // your API key from https://nft.storage/manage

class IPFSStorage {
	constructor(token, endpoint = 'https://api.nft.storage') {
        this.storage = new NFTStorage({ endpoint, token })
	}

	async upload(data) {
		try {
			// const data = await fs.promises.readFile(filePath)
			const cid = await this.storage.storeBlob(new Blob([data]))

			const metadata = {
				name: 'example json',
				description: 'metadata for example json',
				ipfsUrl: `https://${cid}.ipfs.nftstorage.link/`
			}

			const status = await this.storage.status(cid)

			return { cid, status, metadata }
		} catch (error) {
            console.log(error)
			throw new Error('unable to upload file')
		}
	}

	async retrieve(cid) {
		try {
			const status = await this.storage.status(cid)

			if (status.cid) return { ipfsUrl: `https://${cid}.ipfs.nftstorage.link/` }
		} catch (error) {
			throw new Error('file not found')
		}
	}
}

module.exports = new IPFSStorage(token)