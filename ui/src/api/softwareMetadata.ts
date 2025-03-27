import axios from 'axios'

export const getSoftwareMetadata = async (softwareType: string, softwareId: string) => {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/v1/software/search/${softwareId}`, {
        params: {"software_type": softwareType, software_name: softwareId}
    })
    return response.data
}

export const getSoftwareTypes = async () => {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/v1/software/types`)
    return response.data
}