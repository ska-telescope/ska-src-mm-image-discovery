import Box from '@mui/material/Box';
import TitleBar from "./components/TitleBar.tsx";
import SoftwareDiscovery from "./components/SoftwareDiscovery.tsx";
import Sidebar from "./components/Sidebar.tsx";
import {BrowserRouter as Router , Route , Routes} from "react-router-dom";
import ImageDiscovery from "./components/ImageDiscovery.tsx";


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
                    <Route path={"/software/search"} element={<SoftwareDiscovery />}/>
                    <Route path={"/image-discovery/id"} element={<ImageDiscovery  searchType={"id"}/>}/>
                    <Route path={"/image-discovery/type"} element={<ImageDiscovery searchType={"type"}/>}/>


                </Routes>
            </Box>
        </Box>
        </Router>
    );
}
