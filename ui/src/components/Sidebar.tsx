import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import Collapse from "@mui/material/Collapse";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { useState } from "react";
// import { Button } from "@mui/material";
import { Link } from "react-router-dom";

export default function Sidebar() {
    const [openSoftware, setOpenSoftware] = useState(false);
    const [openImage, setOpenImage] = useState(false);

    return (
        <Box sx={{ width: "20%", height: "100%", backgroundColor: "#f5f5f5", borderRight: "1px solid #e0e0e0" }}>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 1, padding: 2 }}>
                <List component="nav">
                    {/* Software Discovery Section */}
                    <ListItemButton onClick={() => setOpenSoftware(!openSoftware)}>
                        <h3>Software Discovery</h3>
                        {openSoftware ? <ExpandLess /> : <ExpandMore />}
                    </ListItemButton>
                    <Collapse in={openSoftware} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                            <ListItemButton component={Link} to="/software/search" sx={{ pl: 4  , color:"#E5096A" }}>
                                GET Software Metadata
                            </ListItemButton>
                        </List>
                    </Collapse>

                    {/* Image Discovery Section */}
                    <ListItemButton onClick={() => setOpenImage(!openImage)}>
                        <h3>Image Discovery</h3>
                        {openImage ? <ExpandLess /> : <ExpandMore />}
                    </ListItemButton>
                    <Collapse in={openImage} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                            <ListItemButton component={Link} to="/image-discovery/id" sx={{ pl: 4 , color:"#E5096A"}}>
                                GET Image by ID
                            </ListItemButton>
                            <ListItemButton component={Link} to="/image-discovery/type" sx={{ pl: 4 , color:"#E5096A" }}>
                                GET Image by Type
                            </ListItemButton>
                        </List>
                    </Collapse>
                </List>
            </Box>
        </Box>
    );
}
