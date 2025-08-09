# BangRak Hackathon 2025 Scoring System Setup

## Environment Variables

This application uses environment variables for secure configuration. Create a `.env` file in the root directory with the following variables:

### Required Environment Variables

```bash
# Password for accessing the scoring system
SCORING_PASSWORD=฿@NGRAK2025by0wenKuj&
```

### Optional Environment Variables

```bash
# Database URL (defaults to SQLite if not set)
DATABASE_URL=postgresql://username:password@host:port/database_name
```

## Setup Instructions

1. **Create a `.env` file** in the root directory of the project
2. **Add the required environment variables** as shown above
3. **Never commit the `.env` file** to version control (it's already in .gitignore)

## Example .env file

```bash
# Copy this to .env and modify as needed
SCORING_PASSWORD=฿@NGRAK2025by0wenKuj&
DATABASE_URL=sqlite:///scores.db
```

## Security Notes

- The `.env` file is automatically ignored by git (see .gitignore)
- Never hardcode passwords in the source code
- Use different passwords for development and production environments
- Regularly rotate passwords in production

## Deployment

For deployment on platforms like Render:

1. Set the environment variables in your deployment platform's dashboard
2. Make sure `SCORING_PASSWORD` is set to your desired password
3. The application will automatically use the environment variable if available, otherwise fall back to the default password
