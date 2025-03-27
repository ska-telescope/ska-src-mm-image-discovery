import {Autocomplete, TextField} from "@mui/material";
import {useQuery} from "@tanstack/react-query";
import {getSoftwareTypes} from "../api/softwareMetadata.ts";

export default function SearchBar() {
    const {data: options = [], isLoading, isError} = useQuery({
        queryKey: ["softwareTypes"],
        queryFn: getSoftwareTypes,
    });
    console.log(options)
    return (
        <Autocomplete
            disabled={isLoading || isError}
            options={options}
            sx={{width: 300}}
            renderInput={(params) => <TextField {...params} label="Software Type"/>}
        />
    )
}