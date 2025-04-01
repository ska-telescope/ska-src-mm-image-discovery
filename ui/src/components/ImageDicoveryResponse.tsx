import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import {materialDark} from 'react-syntax-highlighter/dist/esm/styles/prism';
import Box from "@mui/material/Box";
import {codeString} from "../assets/codeString.ts";
import {ImageMetadata} from "../types/metadataTypes.ts";

interface ResponseSectionProps {
    response?: ImageMetadata;
}

export default function ImageDiscoveryResponse({response}: ResponseSectionProps) {
    return (
        <Accordion>
            <AccordionSummary
                expandIcon={<ArrowDownwardIcon/>}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <Typography component="span" sx={{fontStyle: 'italic', color: 'gray'}}>
                    <strong>{response?.image_id}</strong>
                </Typography>
            </AccordionSummary>
            <AccordionDetails sx={{padding: 5}}>
                <Typography>{response ? "Image Metadata" : "Sample Response"}</Typography>
                <Box sx={{height: 500, width: 900, overflow: 'auto'}}>
                    <SyntaxHighlighter language="json" style={materialDark}>
                        {response ? JSON.stringify(response, null, 2) : codeString}
                    </SyntaxHighlighter>
                </Box>
            </AccordionDetails>
        </Accordion>
    );
}