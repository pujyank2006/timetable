import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Home from "./Home";
import CreateTimetablePage from "./createTimetable/page";
import Dashboard from "./dashboard/page";
import LoginPage from "./login/page";
import TeacherAvailability from "./teacher/availability/page";
import ViewTimetablePage from "./viewTimetable/page";
import Responses from "./response/page";
import InvigulationPage from "./invigilation/page";
import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute";

export default function App() {
  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
      <Routes>
        <Route element={<PublicRoute />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/teacher/availability" element={<TeacherAvailability />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route path="/createtimetable" element={<CreateTimetablePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/viewtimetable" element={<ViewTimetablePage />} />
          <Route path="/responses" element={<Responses />} />
          <Route path="/invigilation" element={<InvigulationPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/login" />} />
        {/* Add more routes */}
      </Routes>
    </>
  );
}
