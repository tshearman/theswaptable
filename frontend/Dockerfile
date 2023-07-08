# Dockerfile

# Use node alpine as it's a small node image
FROM node:18-alpine

# Create the directory on the node image 
# where our Next.js app will live
RUN mkdir -p /app

# Set /app as the working directory
WORKDIR /app

# Copy package.json and package-lock.json
# to the /app working directory
COPY package*.json /app
COPY package.json /app

RUN \
  if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
  else yarn install; \
  fi

# Copy the rest of our Next.js folder into /app
COPY . /app

# Ensure port 3000 is accessible to our system
EXPOSE 3000

ENV PORT 3000

# Run yarn dev, as we would via the command line 
CMD ["yarn", "dev"]
