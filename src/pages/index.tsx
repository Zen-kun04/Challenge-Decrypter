import { useState } from "react"



export default function Home() {

    const [hash, setHash] = useState('');
    const [salt, setSalt] = useState('');
    const [type, setType] = useState('');
    const makeRequest = () => {
        const asynMake = async () => {
            const req = await fetch(`http://127.0.0.1/decrypt?hash=${hash}&`)
        }
    }
    return (
        <main>
            <div className='bg-gray-600 w-1/2 h-auto m-auto mt-20 pt-20 rounded-xl pb-20'>
                <div>
                    <label htmlFor="hash" className="text-center block mb-2 text-sm font-medium text-gray-900 dark:text-white">Hash<span className="text-red-600">*</span></label>
                    <input onChange={e => setHash(e.currentTarget.value)} type="text" id="first_name" className="mb-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 m-auto" placeholder="Your hash" required />
                </div>
                <div>
                    <label htmlFor="salt" className="text-center block mb-2 text-sm font-medium text-gray-900 dark:text-white">Salt</label>
                    <input onChange={e => setSalt(e.currentTarget.value)} type="text" id="first_name" className="mb-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 m-auto" placeholder="Your salt" />
                </div>
                <label htmlFor="underline_select" className="sr-only">Underline select</label>
                <select onChange={e => setType(e.currentTarget.value)} id="underline_select" className="m-auto block py-2.5 px-0 w-64 text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer" required>
                    <option selected>Choose a hash type</option>
                    <option value="SHA256">SHA-256</option>
                    <option value="SHA512">SHA-512</option>
                    <option value="SHA1">SHA1</option>
                    <option value="MD5">MD5</option>
                </select>
                <button className="m-auto block mt-10 bg-green-200 p-2 px-8">Decrypt</button>
                
                

            </div>
            <p>{hash}</p>
            <p>{salt}</p>
            <p>{type}</p>
        </main>
    )
}
