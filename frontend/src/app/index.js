import React from "react";
import AppRedux from "./AppRedux";
import AppRouter from "./AppRouter";
const App = () => {
	return (
		<AppRedux>
				<AppRouter />
		</AppRedux>
	);
};

export default App;
