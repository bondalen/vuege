import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context'

// HTTP link
const httpLink = createHttpLink({
  uri: 'http://localhost:8082/api/graphql'
})

// Auth link
const authLink = setContext((_, { headers }) => {
  // Get token from localStorage if needed
  const token = localStorage.getItem('auth-token')
  
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : ''
    }
  }
})

// Create Apollo client
export function createApolloClient() {
  return new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache({
      typePolicies: {
        Query: {
          fields: {
            // Add field policies here if needed
          }
        }
      }
    }),
    defaultOptions: {
      watchQuery: {
        errorPolicy: 'all'
      },
      query: {
        errorPolicy: 'all'
      }
    }
  })
}
