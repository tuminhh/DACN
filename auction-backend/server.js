const expess = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = expess();

app.user(expess.json());
app.use(cors());

mongoose.connect(process.env.MONGODB_URL)
.then(() => console.log('Connected to MongoDB'))
.catch((err) => console.log(err));

app.get('/', (req, res)=>{
    res.send('API is running...');
})

const PORT = process.env.PORT || 5000;
app.listen(PORT, console.log(`Server running on PORT ${PORT}`));