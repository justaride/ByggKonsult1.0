# Oslo Origo Dataplatform Environment Variables
# Legg disse i din .bashrc, .zshrc eller .env fil

# Metode 1: Client Credentials (for automatiserte systemer)
export OKDATA_CLIENT_ID=your-client-id
export OKDATA_CLIENT_SECRET=your-client-secret

# Metode 2: Username/Password (AD-brukere)
export OKDATA_USERNAME=your-oslo-ad-username
export OKDATA_PASSWORD=your-oslo-ad-password

# Metode 3: API Key (for events)
export OKDATA_API_KEY=your-api-key

# Environment (dev eller prod)
export OKDATA_ENVIRONMENT=dev

# For debugging
export OKDATA_CACHE_CREDENTIALS=false
