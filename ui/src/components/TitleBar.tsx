import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import AppBar from "@mui/material/AppBar";


export default function TitleBar() {
    return (
        <AppBar>
            <Toolbar>
                <Typography variant="h6">SKA SRC MM Image Discovery</Typography>
            </Toolbar>
        </AppBar>
    )
}