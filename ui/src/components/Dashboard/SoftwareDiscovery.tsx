import { Autocomplete, Button, TextField} from "@mui/material";
import {useMutation, useQuery} from "@tanstack/react-query";
import {getSoftwareMetadata, getSoftwareTypes} from "../../api/softwareMetadata.ts";
import Box from "@mui/material/Box";
import {useState} from "react";
import Typography from "@mui/material/Typography";
import {SoftwareDetails} from "../../types/metadataTypes.ts";
import SoftwareDiscoveryResponse from "../Responses/SoftwareDiscoveryResponse.tsx";


export default function SoftwareDiscovery() {
    const {data: options = [], isLoading, isError} = useQuery({
        queryKey: ["softwareTypes"],
        queryFn: getSoftwareTypes,
    });

    const [softwareType, setSoftwareType] = useState<string | null>("");
    const [softwareName, setSoftwareName] = useState<string | null>("");

    const softwareMetadata = useMutation<any, Error, SoftwareDetails>({mutationFn: getSoftwareMetadata});

    return (
        <Box display={"flex"} flexDirection={"column"} gap={3} marginLeft={4}>
            <Box display="flex" flexDirection="row" gap={2} p={2} pl={0}>
                <Autocomplete
                    disabled={isLoading || isError}
                    options={options}
                    sx={{width: 300}}
                    onChange={(_, value: string | null) => setSoftwareType(value)}
                    renderInput={(params) => <TextField {...params} label="Software Type"/>}
                />
                <TextField id="outlined-basic" label="Software name" variant="outlined" sx={{width: 300}}
                           onChange={event => setSoftwareName(event.target.value)}/>
                <Button variant="contained" sx={{ backgroundColor: "#E5096A" }} name={"Search"} loading={softwareMetadata.isPending}
                        onClick={() => softwareMetadata.mutate({
                            softwareType,
                            softwareName
                        })}> Search </Button>
            </Box>

            {softwareMetadata.isError &&
                <Typography color="error">Error: {softwareMetadata.error.message}</Typography>}

            {softwareMetadata.isSuccess && (
                softwareMetadata.data.map((metadata: any, index: number) => (
                    <SoftwareDiscoveryResponse key={index} response={metadata}/>
                )))}


        </Box>
    )
}