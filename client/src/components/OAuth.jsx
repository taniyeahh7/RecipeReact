import { GoogleAuthProvider, getAuth, signInWithPopup } from "firebase/auth";
import { app } from "../firebase";
import { useDispatch } from "react-redux";
import { signInSuccess } from "../redux/user/userSlice";
import { useNavigate } from "react-router-dom";

export default function OAuth() {
	const dispatch = useDispatch();
	const navigate = useNavigate();

	//function to handle google auth
	const handleGoogleClick = async () => {
		try {
			const provider = new GoogleAuthProvider();
			const auth = getAuth(app);

			const result = await signInWithPopup(auth, provider);

			const res = await fetch("/api/auth/google", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					name: result.user.displayName,
					email: result.user.email,
				}),
			});
			const data = await res.json();
			dispatch(signInSuccess(data));
			navigate("/choice");
		} catch (error) {
			console.log("could not sign in with google", error);
		}
	};
	// ----- front-end code -----
	return (
		<button onClick={handleGoogleClick} type="submit">
			Continue with google
		</button>
	);
}