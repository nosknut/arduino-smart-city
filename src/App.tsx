import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { PageNavigation } from './components/PageNavigation';
import { CityScreen } from './screens/CityScreen';

function App() {
  return (
    <BrowserRouter>
      <PageNavigation />
      <Routes>
        <Route path="/" element={<CityScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
