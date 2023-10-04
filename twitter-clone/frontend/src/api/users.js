import { axi } from './userAxios';

export const loginReq = async (data) => {
  await axi.post('/users/login/', data);
};
