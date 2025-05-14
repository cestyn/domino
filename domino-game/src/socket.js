import { io } from "socket.io-client";
const socket = io("https://domino-qb1h.onrender.com", {
  transports: ["websocket"],
});
export default socket;
