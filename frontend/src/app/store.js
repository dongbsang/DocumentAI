import { configureStore } from '@reduxjs/toolkit';
import rootReducer from '../redux/reducer'; // reducer/index.js
import createSagaMiddleware from 'redux-saga';
import rootSaga from '../redux/saga'; // saga/index.js

const sagaMiddleware = createSagaMiddleware();

const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ thunk: false }).concat(sagaMiddleware),
});

sagaMiddleware.run(rootSaga);

export default store;