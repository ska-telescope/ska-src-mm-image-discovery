import axios from 'axios'
import {SoftwareDetails, SoftwareMetadata} from "../types/metadataTypes.ts";


export const getSoftwareMetadata = async (softwareMetadata: SoftwareDetails) => {
    const response = await axios.get<SoftwareMetadata>(`${import.meta.env.VITE_BASE_URL}/v1/software/search/`, {
        params: {"software_type": softwareMetadata.softwareType, software_name: softwareMetadata.softwareName},
    })
    console.log(response.data)
    return response.data
}

export const getSoftwareTypes = async () => {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/v1/software/types`)
    return response.data
}