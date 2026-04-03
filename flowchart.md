```mermaid
flowchart TD                                                                                                                                
      A([User Preferences\nfavorite_mood · favorite_genre\ntarget_energy · target_acousticness\ntarget_danceability · target_valence])        
                                                                                                                                              
      B[Load songs.csv\n20 songs]                                                                                                             
                                                                                                                                              
      A --> LOOP                                                                                                                              
      B --> LOOP                                                                                                                              
                                                                                                                                              
      subgraph LOOP["The Loop — repeat for every song"]                                                                                       
          C[Pick next song] --> D
                                                                                                                                              
          subgraph SCORE["Scoring Rule"]                                                                                                      
              D{mood\nmatches?}
              D -- yes --> D1[+2.0 pts]                                                                                                       
              D -- no  --> D2[+0.0 pts]                                                                                                       
   
              E{genre\nmatches?}                                                                                                              
              E -- yes --> E1[+1.5 pts]                     
              E -- no  --> E2[+0.0 pts]                                                                                                       
                                                            
              F["energy proximity\n2.0 × (1 − |song − user|)"]                                                                                
              G["acousticness proximity\n1.5 × (1 − |song − user|)"]
              H["danceability proximity\n1.0 × (1 − |song − user|)"]                                                                          
              I["valence proximity\n0.5 × (1 − |song − user|)"]                                                                               
   
              D1 & D2 --> E                                                                                                                   
              E1 & E2 --> F --> G --> H --> I               
          end                                                                                                                                 
                                                            
          I --> J[Sum all points\nmax = 8.5]                                                                                                  
          J --> K[Store song + score]
      end                                                                                                                                     
                                                            
      K --> L{More songs?}                                                                                                                    
      L -- yes --> C
      L -- no  --> M                                                                                                                          
                                                            
      subgraph RANK["Ranking Rule"]
          M[Sort all scores\ndescending]
          M --> N[Slice top K results]                                                                                                        
      end
                                                                                                                                              
      N --> O([Output\nTop K recommendations\nwith scores + explanation])                                                                     
```
