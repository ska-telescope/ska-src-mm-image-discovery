import { useMutation } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import { Button, TextField } from "@mui/material";
import Typography from "@mui/material/Typography";
import { getImageById, getImagebyType } from "../api/ImageMetadata";
import ImageDiscoveryResponse from "./ImageDicoveryResponse.tsx";
import { useParams } from "react-router-dom";


export default function ImageDiscovery() {
    const [searchParam, setSearchParam] = useState<string>("");
    const { searchType } = useParams<{ searchType: "id" | "type" }>();

    const softwareMetadata = useMutation<any, Error, string>({
        mutationFn: searchType === "id" ? getImageById : getImagebyType
    });

    useEffect(() => {
        softwareMetadata.reset();
        setSearchParam("");
    }, [searchType]);

    return (
        <Box display={"flex"} flexDirection={"column"} gap={3} marginLeft={4}>
            <Box display="flex" flexDirection="row" gap={2} p={2} pl={0}>
                <TextField id="outlined-basic" label={searchType === "type" ? "Software type" : "Software Id"}
                           variant="outlined" sx={{ width: 300 }}
                           onChange={event => setSearchParam(event.target.value)} />

                <Button variant="contained" sx={{ backgroundColor: "#E5096A" }} name={"Search"}
                        loading={softwareMetadata.isPending}
                        onClick={() => {
                            softwareMetadata.mutate(searchParam);
                        }}> Search </Button>
            </Box>

            {softwareMetadata.isError &&
                <Typography color="error">Error: {softwareMetadata.error.message}</Typography>}

            {softwareMetadata.isSuccess && (
                searchType === "id" ? (
                    <ImageDiscoveryResponse response={softwareMetadata.data} />
                ) : (
                    Array.isArray(softwareMetadata.data) ? (
                        softwareMetadata.data.map((metadata: any, index: number) => (
                            <ImageDiscoveryResponse key={index} response={metadata} />
                        ))
                    ) : (
                        <Typography color="error">Unexpected response format</Typography>
                    )
                )
            )}
        </Box>
    );
}