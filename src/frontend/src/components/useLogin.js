import { ref } from '@vue/reactivity'
//import { projectAuth } from '../firebase/config'
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:8000/';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

const error = ref(null)

const login = async (email, password) => {
  error.value = null
  try {
    const baseURL = 'http://localhost:8000/';
    const formData = new FormData();
    formData.append('grant_type', 'password');
    formData.append('username', email);
    formData.append('password', password);
    console.log(baseURL + 'auth/token')
    axios.post(baseURL + 'auth/token', formData).then((res) => {
      if (res && res.data) {
        console.log(res);
        return res
      }
    })
  } catch(err) {
    console.log(err.message);
    error.value = 'Incorrect login credentials'
  }
}

const useLogin = () => {
  return {error, login}
}

export default useLogin
