import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { MainLayout } from './layouts/MainLayout';
import {
  Home,
  Login,
  Signup,
  Packages,
  Preferences,
  Subscribe,
  SubscriptionSuccess
} from './pages';
import { PrivacyPolicy, Terms } from './pages/legal';
import RoadTestGuide from './pages/guides/RoadTestGuide';

export default function App() {
  return (
    <HelmetProvider>
      <Router>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/guides" element={<RoadTestGuide />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/packages" element={<Packages />} />
            <Route path="/preferences" element={<Preferences />} />
            <Route path="/subscribe/:packageId" element={<Subscribe />} />
            <Route path="/subscription/success" element={<SubscriptionSuccess />} />
            <Route path="/privacy" element={<PrivacyPolicy />} />
            <Route path="/terms" element={<Terms />} />
          </Routes>
        </MainLayout>
      </Router>
    </HelmetProvider>
  );
}