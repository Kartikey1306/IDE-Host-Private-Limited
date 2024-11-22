The application will be available at `http://localhost:5000`.

## Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to "APIs & Services" > "Credentials".
4. Click "Create Credentials" and select "OAuth client ID".
5. Choose "Web application" as the application type.
6. Add `http://localhost:5000/login/google/authorized` to the authorized redirect URIs.
7. Copy the Client ID and Client Secret and add them to your `.env` file.

## Usage

1. Register for an account or log in with Google.
2. Use the dashboard to scrape new web content or generate prompts.
3. View your scraped data and generated prompts on the dashboard.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

