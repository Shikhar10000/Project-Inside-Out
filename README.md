# Project Inside Out
### Summon Your Emotions!
In today’s hyper active world full of stress and pressure, mental and emotional health is becoming important factors in maintaining a person’s well-being, but with the ever increasing work and social load, people don’t have enough time to take care of themselves, especially their mental health. There is enormous amount of studies that showcase that the ambient lighting and music have a major impact on the mood. So, our solution to is to track the persons emotions using a network of cameras and set the lighting theme, music and ambiance in accordance to the mood of person and then gradually moving them to the more positive moods to try to improve the mood of the person.
So just like our [previous open source project](https://github.com/kaiwalya4850/Direct_Democracy), we plan to make this project open source too! 
The research paper on this would be published soon, and we would add the link for the same for model architecture references!

## Usage

The trained model on 7 different emotions, with an accuracy of 74% is under models folder. The harcasdade file is for detection of front face, so first face is detected then the mood is detected. The model is named

```bash
emotion_model.hdf5
```
If you would like to retrain the model, all the scripts can be found under training folder. We have included scripts that work on a recorded video as well as on webcam.

To play the songs according to mood via Spotify Player, use the file:
```bash
emotion.py
```
Feel free to change the ranges for specific moods!

Now since we allocate a score to each identified mood and store it in Firestore, the file to do this part is:
```bash
emotions.py
```
So the process goes like, run emotions.py send data to firestore, the emotion.py gets the data and auto logins in Spotify and starts playing the song.
For Firestore structure we have the files:
```bash
fire.py
firestore.py
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
