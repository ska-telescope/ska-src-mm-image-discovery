import Box from '@mui/material/Box';
import TitleBar from "./components/Header/TitleBar.tsx";
import SoftwareDiscovery from "./components/Dashboard/SoftwareDiscovery.tsx";
import Sidebar from "./components/Sidebar/Sidebar.tsx";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import ImageDiscovery from "./components/Dashboard/ImageDiscovery.tsx";


export default function App() {
    return (
        <Router>
            <Box sx={{width: "100vw", height: "100vh", flexGrow: 1}}>
                <TitleBar/>
                <Box sx={{
                    display: "flex",
                    flexDirection: {xs: "column", sm: "row"},
                    flexGrow: 1,
                    height: "100%"
                }}>
                    <Sidebar/>
                    <Routes>
                        <Route path={"/web"} element={<SoftwareDiscovery/>}/>
                        <Route path={"/web/image-discovery/:searchType"} element={<ImageDiscovery/>}/>
                    </Routes>
                </Box>
            </Box>
        </Router>
    );
}
