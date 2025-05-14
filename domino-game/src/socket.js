import { io } from "socket.io-client";
const socket = io("http://localhost:8000"); // Updated Python server URL
export default socket;
