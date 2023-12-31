import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";

import Navbar from "./components/Navbar.jsx";
// import ChefSection from "./components/ChefSection.js"; if want to include put in body also
// import Footer from "./components/Footer.js";
import Home from "./pages/Home.js";
import Recipes from "./pages/Recipes.js";
import Settings from "./pages/Settings.js";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import Choice from "./pages/Choice.js";
import ExerciseChoice from "./pages/ExerciseChoice.js";
import IngredientForm from "./pages/IngredientForm.js";
import FilterRecipe from "./pages/FilterRecipe.js";

function App() {
	return (
		<Router>
			<Navbar />
			<div className="container main">
				<Routes>
					<Route path="/" element={<Home />} />
					<Route path="/recipes" element={<Recipes />} />
					<Route path="/settings" element={<Settings />} />
					<Route path="/login" element={<Login />} />
					<Route path="/signup" element={<Signup />} />

					<Route element={<PrivateRoute />}>
						<Route path="/choice" element={<Choice />} />
						<Route path="/exercisechoice" element={<ExerciseChoice />} />
						<Route path="/ingredientform" element={<IngredientForm />} />
						<Route path="/filterrecipe" element={<FilterRecipe />} />
					</Route>
				</Routes>
			</div>
		</Router>
	);
}

export default App;
