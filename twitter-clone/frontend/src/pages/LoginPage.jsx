import { useMutation, useQueryClient } from '@tanstack/react-query';
import { loginReq } from '../api/users';
import { Formik, Field, Form } from 'formik';
import { Link, useNavigate } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: loginReq,
    onSuccess: () => {
      queryClient.invalidateQueries('tweets');
      navigate('/');
      console.log('loginMutation success');
    },
    onError: (error) => {
      console.error(error);
    },
  });

  return <div>LoginPage</div>;
}

export default LoginPage;
