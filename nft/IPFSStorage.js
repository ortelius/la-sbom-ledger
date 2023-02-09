const fs = require('fs')
const { NFTStorage, Blob } = require('nft.storage')
const https = require('https')

const token =
	process.env.NFT_STORAGE_API_TOKEN ||
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk3ODMwMGIzNUMzOEM3NzMxYWNDNjk4NDFiODU4NDNiRmIxRjExN0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY0ODY2MjM1MDcwNiwibmFtZSI6Im9ydGVsaXVzX3Nib21fbGVkZ2VyX2RlbW8ifQ.egQzHqDB83UoK7ynE4fn4dhgIKWLhPP1B9E6qey4KHM' // your API key from https://nft.storage/manage

class IPFSStorage {
	constructor(token, endpoint = 'https://api.nft.storage') {
		this.storage = new NFTStorage({ endpoint, token })
	}

	async upload(filePath) {
		try {
			const data = this.#minify(filePath)
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

			if (status.cid) {
				await this.#transposeNFTToSBOMFile(
					`https://${cid}.ipfs.nftstorage.link/`,
					cid
				)
			}
		} catch (error) {
			throw new Error('file not found')
		}
	}

	async #transposeNFTToSBOMFile(url, filename) {
		let file = fs.createWriteStream(`${filename}.json`)

		try {
			https.get(url, (response) => {
				response
					.on('finish', () => {
						fs.readFile(`${filename}.json`, { encoding: 'utf8' })
					})
					.pipe(file)
			})
		} catch (error) {
			console.log('an error occurred whilst tranposing nft to sbom', error)
		}
	}

	async #minify(filePath) {
		try {
			const data = JSON.parse((await fs.promises.readFile(filePath)).toString())
			return Buffer.from(JSON.stringify(data, null, 0), 'utf-8')
		} catch (error) {
			console.log(error)
			throw new console.error('unable to minify file')
		}
	}
}

let ipfsStorage = new IPFSStorage(token)

async function test() {
	await ipfsStorage.retrieve(
		'bafkreigqcgfdjwzcfl2vl2fw3djw2u63m3k663zghrrqwntaqgxldkzgdm'
	)
}

test()

module.exports = new IPFSStorage(token)
