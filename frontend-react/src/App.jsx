import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./Home";
import CreateTimetablePage from "./createTimetable/page";
import Dashboard from "./dashboard/page";
import LoginPage from "./login/page";
import TeacherAvailability from "./teacher/availability/page";
import ViewTimetablePage from "./viewTimetable/page";
import Responses from "./response/page";
import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute";

export default function App() {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPage />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path="/createtimetable" element={<CreateTimetablePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/teacher/availability" element={<TeacherAvailability />} />
        <Route path="/viewtimetable" element={<ViewTimetablePage />} />
        <Route path="/responses" element={<Responses />} />
      </Route>

      <Route path="*" element={<Navigate to="/login" />} />
      {/* Add more routes */}
    </Routes>
  );
}
