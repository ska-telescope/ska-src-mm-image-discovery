import Box from '@mui/material/Box';
import TitleBar from "./components/TitleBar.tsx";
import Dashboard from "./components/Dashboard.tsx";

export default function App() {
    return (
        <Box sx={{width: "100vw", height: "100vh", flexGrow: 1}}>
            <TitleBar/>
            <Box sx={{ flexGrow: 1, paddingTop: "100px", display: "flex", justifyContent: "center", alignItems: "center" }}>
                <Dashboard/>
            </Box>
        </Box>
    );
}
