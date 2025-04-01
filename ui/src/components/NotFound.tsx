import { Box, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function NotFoundPage() {
    const navigate = useNavigate();

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                height: "100vh",
                textAlign: "center",
            }}
        >
            <Typography variant="h1" sx={{ fontSize: "6rem", fontWeight: "bold" }}>
                404
            </Typography>
            <Typography variant="h5" sx={{ mb: 2 }}>
                Oops! The page you're looking for doesn't exist.
            </Typography>
            <Button variant="contained" onClick={() => navigate("/")}>
                Go Home
            </Button>
        </Box>
    );
}