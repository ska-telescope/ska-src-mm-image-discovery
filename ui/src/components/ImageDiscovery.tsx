import {useMutation} from "@tanstack/react-query";
import {useState} from "react";
import Box from "@mui/material/Box";
import {Button, TextField} from "@mui/material";
import Typography from "@mui/material/Typography";
import {getImageById, getImagebyType} from "../api/ImageMetadata.ts";
import ImageDiscoveryResponse from "./ImageDicoveryResponse.tsx";

interface ImageDiscoveryProps {
    searchType: "id" | "type";
}

export default function ImageDiscovery({searchType}: ImageDiscoveryProps) {
    const [searchParam, setSearchParam] = useState<string>("");

    const softwareMetadata = useMutation<any, Error, string>({
        mutationFn: searchType === "id" ? getImageById : getImagebyType
    });

    return (
        <Box display={"flex"} flexDirection={"column"} gap={3}>
            <Box display="flex" flexDirection="row" gap={2} p={2} pl={0}>
                <TextField id="outlined-basic" label={searchType === "type" ? "Software type" : "Software Id"}
                           variant="outlined" sx={{width: 300}}
                           onChange={event => setSearchParam(event.target.value)}/>

                <Button variant="contained" sx={{backgroundColor: "#E5096A"}} name={"Search"}
                        loading={softwareMetadata.isPending}
                        onClick={() => {
                            softwareMetadata.mutate(searchParam);
                        }}> Search </Button>
            </Box>

            {softwareMetadata.isError &&
                <Typography color="error">Error: {softwareMetadata.error.message}</Typography>}


            {softwareMetadata.isSuccess && (
                searchType === "id" ? (
                    console.log('Software Metadata:', softwareMetadata.data),
                        <ImageDiscoveryResponse response={softwareMetadata.data}/>
                ) : (
                    softwareMetadata.data.map((metadata: any, index: number) => (
                        console.log('Software Metadata:', metadata),
                            <ImageDiscoveryResponse key={index} response={metadata}/>
                    ))
                )
            )}
        </Box>
    );
}