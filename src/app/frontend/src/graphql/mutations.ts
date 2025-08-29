import { gql } from '@apollo/client/core'

// Мутации для организаций
export const CREATE_ORGANIZATION = gql`
  mutation CreateOrganizationalUnit($input: OrganizationalUnitInput!) {
    createOrganizationalUnit(input: $input) {
      id
      name
      type
      foundedDate
      dissolvedDate
    }
  }
`

export const UPDATE_ORGANIZATION = gql`
  mutation UpdateOrganizationalUnit($id: ID!, $input: OrganizationalUnitInput!) {
    updateOrganizationalUnit(id: $id, input: $input) {
      id
      name
      type
      foundedDate
      dissolvedDate
    }
  }
`

export const DELETE_ORGANIZATION = gql`
  mutation DeleteOrganizationalUnit($id: ID!) {
    deleteOrganizationalUnit(id: $id)
  }
`

// Мутации для должностей
export const CREATE_POSITION = gql`
  mutation CreatePosition($input: PositionInput!) {
    createPosition(input: $input) {
      id
      title
      hierarchy
      responsibilities
      isActive
      organization {
        id
        name
      }
      createdDate
      abolishedDate
    }
  }
`

export const UPDATE_POSITION = gql`
  mutation UpdatePosition($id: ID!, $input: PositionInput!) {
    updatePosition(id: $id, input: $input) {
      id
      title
      hierarchy
      responsibilities
      isActive
      organization {
        id
        name
      }
      createdDate
      abolishedDate
    }
  }
`

export const DELETE_POSITION = gql`
  mutation DeletePosition($id: ID!) {
    deletePosition(id: $id)
  }
`

// Мутации для государств
export const CREATE_STATE = gql`
  mutation CreateState($input: CreateStateInput!) {
    createState(input: $input) {
      id
      name
      code
      type
      description
      foundedDate
      dissolvedDate
      capital {
        id
        name
      }
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_STATE = gql`
  mutation UpdateState($id: ID!, $input: UpdateStateInput!) {
    updateState(id: $id, input: $input) {
      id
      name
      code
      type
      description
      foundedDate
      dissolvedDate
      capital {
        id
        name
      }
      updatedAt
    }
  }
`

export const DELETE_STATE = gql`
  mutation DeleteState($id: ID!) {
    deleteState(id: $id) {
      id
      name
    }
  }
`

// Мутации для людей
export const CREATE_PERSON = gql`
  mutation CreatePerson($input: CreatePersonInput!) {
    createPerson(input: $input) {
      id
      firstName
      lastName
      middleName
      birthDate
      deathDate
      biography
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_PERSON = gql`
  mutation UpdatePerson($id: ID!, $input: UpdatePersonInput!) {
    updatePerson(id: $id, input: $input) {
      id
      firstName
      lastName
      middleName
      birthDate
      deathDate
      biography
      updatedAt
    }
  }
`

export const DELETE_PERSON = gql`
  mutation DeletePerson($id: ID!) {
    deletePerson(id: $id) {
      id
      firstName
      lastName
    }
  }
`

// Мутации для мест
export const CREATE_LOCATION = gql`
  mutation CreateLocation($input: CreateLocationInput!) {
    createLocation(input: $input) {
      id
      name
      type
      latitude
      longitude
      parentLocation {
        id
        name
      }
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_LOCATION = gql`
  mutation UpdateLocation($id: ID!, $input: UpdateLocationInput!) {
    updateLocation(id: $id, input: $input) {
      id
      name
      type
      latitude
      longitude
      parentLocation {
        id
        name
      }
      updatedAt
    }
  }
`

export const DELETE_LOCATION = gql`
  mutation DeleteLocation($id: ID!) {
    deleteLocation(id: $id) {
      id
      name
    }
  }
`