import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice({
	initialState: {
		logined: localStorage.getItem("adm-usr") ? true : false,
		token: decodeURIComponent(escape(atob(localStorage.getItem("adm-usr") ?? ""))) ?? "",
	},
	name: "user",
	reducers: {
		login: (draft, { payload }) => {
			draft.logined = true;
			draft.token = payload;
			localStorage.setItem("adm-usr", btoa(unescape(encodeURIComponent(payload))));
			return draft;
		},
		logout: (draft, { payload }) => {
			draft.logined = false;
			draft.token = "";
			localStorage.removeItem("adm-usr");
			return draft;
		},
	},
});

export const { login, logout } = userSlice.actions;
export default userSlice.reducer;
