import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import AppBar from "@mui/material/AppBar";


export default function TitleBar() {
    return (
        <AppBar sx={{ backgroundColor: "#E5096A" , position: "sticky", top: 0, width: "100%" }}>
            <Toolbar>
                <Typography variant="h6" fontWeight="bold" fontFamily="monospace">SKA SRC MM Image Discovery</Typography>
            </Toolbar>
        </AppBar>
    )
}