import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import reportWebVitals from './reportWebVitals';
import './index.css';
import Flauta from "./flauta/Flauta";
import Numeros from "./numeros/Numeros";

const root = ReactDOM.createRoot(document.getElementById('root'));

const urlModelFlauta = `${window.location.origin}/flauta/model/`;
const urlModelNumeros = `${window.location.origin}/numeros/model/`;

const flautaMaxNumberOfHits = 6;
const numerosMaxNumberOfHits = {cero: 2, uno: 3};

root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/flauta" element={<Flauta url={urlModelFlauta} maxNumberOfHits={flautaMaxNumberOfHits}/>}/>
                <Route path="/numeros" element={<Numeros url={urlModelNumeros} maxNumberOfHits={numerosMaxNumberOfHits}/>}/>
            </Routes>
        </BrowserRouter>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
