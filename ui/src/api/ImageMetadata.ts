
import {ImageMetadata} from "../types/metadataTypes.ts";
import axios from "axios";



export const getImageById = async (id: string) => {
    const params = {"image_id": id};
    const response = await axios.get<ImageMetadata>(`${import.meta.env.VITE_BASE_URL}/v1/image/fetch` , {params})
    console.log(response.data)
    return response.data
}

export const getImagebyType = async (type: string) => {
    const params = {"type_name": type};
    const response = await axios.get<ImageMetadata>(`${import.meta.env.VITE_BASE_URL}/v1/image/search` , {params})
    console.log(response.data)
    return response.data
}

