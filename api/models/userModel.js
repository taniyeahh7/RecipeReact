const mongoose = require("mongoose"); // Erase if already required
const bcrypt = require("bcrypt");
const crypto = require("crypto");

// Declare the Schema of the Mongo model
var userSchema = new mongoose.Schema(
	{
		firstname: {
			type: String,
			required: true,
			unique: true,
			index: true,
		},
		lastname: {
			type: String,
			required: true,
			index: true,
		},
		email: {
			type: String,
			required: true,
			unique: true,
		},
		mobile: {
			type: String,
			required: true,
			unique: true,
		},
		password: {
			type: String,
			required: true,
		},
		role: {
			type: String,
			default: "user",
		},
		isBlocked: {
			type: Boolean,
			default: false,
		},
		refreshToken: {
			type: String,
		},
		passwordChangedAt: Date,
		passwordResetToken: String,
		passwordResetExpires: Date,
	},
	{
		timestamps: true, // Enable automatic timestamps
	}
);

//encrypts the password after entry is saved
userSchema.pre("save", async function (next) {
	if (!this.isModified("password")) {
		next();
	}
	const salt = bcrypt.genSaltSync(10);
	this.password = await bcrypt.hash(this.password, salt);
	next();
});

//method to match passwords
userSchema.methods.isPasswordMatched = async function (enteredPassword) {
	return await bcrypt.compare(enteredPassword, this.password);
};

//method to create PasswordResetToken
userSchema.methods.createPasswordResetToken = async function () {
	const resetToken = crypto.randomBytes(32).toString("hex");
	this.passwordResetToken = crypto
		.createHash("sha256")
		.update(resetToken)
		.digest("hex");
	this.passwordResetExpires = Date.now() + 60 * 10000; //10 mins
	return resetToken;
};

//Export the model
module.exports = mongoose.model("User", userSchema);
