namespace MugEngineTemplate
{
	enum GInput
	{
		MoveLeft,
		MoveRight,
		Jump,
		Confirm,

#if DEBUG
		DebugCameraToggle,
		DebugCameraZoom,
		DebugCameraUp,
		DebugCameraDown,
		DebugCameraLeft,
		DebugCameraRight
#endif // DEBUG
	}

	static class InputConfig
	{
#if DEBUG
		public static readonly MDirPad<GInput> DebugCamDPad = new(GInput.DebugCameraUp, GInput.DebugCameraDown, GInput.DebugCameraLeft, GInput.DebugCameraRight);
#endif // DEBUG

		public static void SetDefaultButtons()
		{
			// Arrow keys or WASD
			MugInput.I.BindButton(GInput.MoveLeft, new MKeyboardButton(Keys.Left), new MKeyboardButton(Keys.A));
			MugInput.I.BindButton(GInput.MoveRight, new MKeyboardButton(Keys.Right), new MKeyboardButton(Keys.D));

			// Jump
			MugInput.I.BindButton(GInput.Jump, new MKeyboardButton(Keys.Space));

			// Confirm
			MugInput.I.BindButton(GInput.Confirm, new MKeyboardButton(Keys.Enter));
		}
	}
}
