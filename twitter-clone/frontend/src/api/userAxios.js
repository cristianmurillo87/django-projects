import axios from 'axios';
import jwt_decode from 'jwt-decode';

const baseURL = 'http://localhost:8000';

export const axi = axios.create({
  baseURL,
});
