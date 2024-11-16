# Use a lightweight Node.js image as the base
FROM node:18-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy only package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js app
RUN npm run build

# Start the Next.js server
EXPOSE 3000
CMD ["npm", "run", "start"]

