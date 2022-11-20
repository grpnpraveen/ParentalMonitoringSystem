import cv2

""" Identification """

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

faceNet=cv2.dnn.readNet(faceModel, faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(12-18)', '(18-30)', '(30-45)', '(45-52)', '(55-100)']
genderList = ['Male', 'Female']
padding=20


gender_major = dict()
gender_major['Male']=0
gender_major['Female']=0
age_major = dict()
age_major['>18']=0
age_major['<18']=0

""" Face highliting """

def faceBox(faceNet, frames):
    frameHeight=frames.shape[0]
    frameWidth=frames.shape[1]
    blob=cv2.dnn.blobFromImage(frames, 1.0, (300,300), [104,117,123], swapRB=False)
    faceNet.setInput(blob)
    detection=faceNet.forward()
    bboxs=[]
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>0.7:
            x1=int(detection[0,0,i,3]*frameWidth)
            y1=int(detection[0,0,i,4]*frameHeight)
            x2=int(detection[0,0,i,5]*frameWidth)
            y2=int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1,y1,x2,y2])
            cv2.rectangle(frames, (x1,y1),(x2,y2),(0,255,0), 1)
    return frames, bboxs

""" Video display """

def DisplayVid(frame):

    epochs=0
    limit=1

    # while (True):
    # frame = cv2.imread("t2.jpg")
    frame = cv2.imread(frame)
    frameFace, bboxes = faceBox(faceNet, frame)

    for bbox in bboxes:
        face = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        try:
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            if(gender == 'Male'):
                gender_major['Male'] = gender_major['Male']+1
            else:
                gender_major['Female'] = gender_major['Female']+1
                
            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            # age = ageList[agePreds[0].argmax()]
            if(agePreds[0].argmax()>=4):
                age = "Above 18"
                age_major['>18'] = age_major['>18']+1
            else:
                age = "Below 18"
                age_major['<18'] = age_major['<18']+1

            label = "{}, {}".format(gender, age)
            # print(label)
            epochs=epochs+1
            if(epochs>limit):
                break
            cv2.rectangle(frameFace, (bbox[0], bbox[1] - 30), (bbox[2], bbox[1]), (0, 255, 0), -1)
            cv2.putText(frameFace, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2,
                        cv2.LINE_AA)
        except:
            pass
        # if(epochs>limit):
        #     break
        # # cv2.imshow("Age-Gender", frameFace)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
    # cv2.destroyAllWindows()

def FinalPrediction(image=None):
    if image!=None:
        DisplayVid(image)

        if(gender_major['Male']>gender_major['Female']):
            g = 'Male'
        else:
            g = 'Female'

        if(age_major['>18']>age_major['<18']):
            a = 'Above 18'
        else:
            a = 'Below 18'
        print('Final Prediction: {}, {}'.format(g, a))
        return [True,"successfully detected",a]
    else:
        return [False,"invalid image",-1]

# FinalPrediction('t2.jpg')