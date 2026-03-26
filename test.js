import http from 'k6/http';

export const options = {
  vus: 100,
  duration: '30s',
};

export default function () {
  http.get('https://isikakd.github.io/AI-Yemek-Tavsiyesi/');
}
