try:
  import ujson as json
except:
  import json as json
from copy import deepcopy as deepcopy

''' ---- Loading settings begins here ---- '''

teams={}
with open('teams.json','r') as teamListingFile:
  teams=json.loads(teamListingFile.read())
currentTeam=0
currentMatchNo=1
currentSuffix='r1'

scoring={}
with open('scoring.json','r') as scoringFile:
  scoring=json.loads(scoringFile.read())['fieldScoring']
print scoring[0]

import wx


class Client(wx.Frame):
  def __init__(self, parent, title):
    super(Client, self).__init__(parent, title=title, 
        size=(800, 400))
        
    matchSetupPanel = wx.Panel(self)

    sizer = wx.BoxSizer(wx.HORIZONTAL)

    vbox = wx.BoxSizer(wx.VERTICAL)
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    l = wx.StaticText(matchSetupPanel, label='Team #', style=wx.ALIGN_LEFT)
    hbox.Add(l, flag=wx.ALL, border=15)
    teamSelection = wx.ComboBox(matchSetupPanel, choices=[t+': '+teams[t] for t in sorted(teams.keys(), key=int)], style=wx.CB_READONLY|wx.ALIGN_RIGHT)
    teamSelection.Bind(wx.EVT_COMBOBOX, self.OnTeamSelect)
    hbox.Add(teamSelection, flag=wx.ALL, border=15)
    vbox.Add(hbox, flag=wx.ALL, border=0)

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    l = wx.StaticText(matchSetupPanel, label='Match #', style=wx.ALIGN_LEFT)
    hbox.Add(l, flag=wx.ALL, border=15)
    self.matchNumberSelection = wx.SpinCtrl(matchSetupPanel, value='0', size=(60,-1), style=wx.CB_READONLY|wx.ALIGN_RIGHT)
    self.matchNumberSelection.SetRange(0,70)
    self.matchNumberSelection.Bind(wx.EVT_SPINCTRL, self.OnMatchNoSelect)
    hbox.Add(self.matchNumberSelection, flag=wx.ALL, border=15)
    vbox.Add(hbox, flag=wx.ALL, border=0)



    hbox = wx.BoxSizer(wx.HORIZONTAL)
    l = wx.StaticText(matchSetupPanel, label='Robot #', style=wx.ALIGN_LEFT)
    hbox.Add(l, flag=wx.ALL, border=15)
    robotStationSelection = wx.ComboBox(matchSetupPanel, choices=['RED 1', 'RED 2', 'RED 3', 'BLU 1', 'BLU 2', 'BLU 3'], style=wx.CB_READONLY|wx.ALIGN_RIGHT)
    robotStationSelection.Bind(wx.EVT_COMBOBOX, self.OnRobotStationSelect)
    hbox.Add(robotStationSelection, flag=wx.ALL, border=15)
    vbox.Add(hbox, flag=wx.ALL, border=0)
    
    button=wx.Button(matchSetupPanel, label='Save Round', size=(220,45))
    button.Bind(wx.EVT_BUTTON, self.OnSubmit)
    vbox.Add(button, flag=wx.ALL, border=15)

    sizer.Add(vbox, flag=wx.ALL, border=3)

    vbox = wx.FlexGridSizer(len(scoring), 2, 2, 10)
    self.widgets = []
    for scoreMethod in scoring:
      #hbox = wx.BoxSizer(wx.HORIZONTAL)
      #hbox.Add(, border=1)
      vbox.Add(wx.StaticText(matchSetupPanel, label=scoreMethod[0]), flag=wx.ALL, border=10)
      if isinstance(scoreMethod[1], list):
        self.widgets.append(wx.ComboBox(matchSetupPanel, choices=scoreMethod[1], name=scoreMethod[0]))
        vbox.Add(self.widgets[-1], flag=wx.ALL, border=10)
      elif scoreMethod[1].lower() in ['y/n', 'yn', 'truefalse', 'bool', 'boolean', 'yesno', 'yes/no']:
        self.widgets.append(wx.ToggleButton(matchSetupPanel, label='   !   ', size=(60,-1), name=scoreMethod[0]))
        vbox.Add(self.widgets[-1], flag=wx.ALL, border=10)
      elif scoreMethod[1].lower() in ['str', 'string', 'text', 'words', 'longstr', 'longstring', 'varchar']:
        # Make a string entry box
        self.widgets.append(wx.TextCtrl(matchSetupPanel, size=(200,-1), name=scoreMethod[0]))
        vbox.Add(self.widgets[-1], flag=wx.ALL, border=10)
      else:
        # Make a number entry box
        self.widgets.append(wx.SpinCtrl(matchSetupPanel, value='0', size=(60,-1), name=scoreMethod[0]))
        self.widgets[-1].SetRange(-99,99)
        vbox.Add(self.widgets[-1], border=10)
      #vbox.Add(hbox, flag=wx.ALL, border=2)
    sizer.Add(vbox, flag=wx.ALL, border=3)

    matchSetupPanel.SetSizer(sizer)

    self.Move((70,10))
    self.Show()

  def OnTeamSelect(self, e):
    global currentTeam
    currentTeam=e.GetString()
  def OnSubmit(self, e):
    # Write info to dropbox, clear out the input boxes
    with open('matches/q-'+str(self.matchNumberSelection.GetValue())+'-'+currentSuffix+'.json', 'w') as matchFile:
      info = {"teamNo":str(currentTeam).split(':')[0]}
      for w in range(len(self.widgets)):
        info[scoring[w][0]] = self.widgets[w].GetValue()
        try:
          self.widgets[w].SetValue(0)
        except:
          try:
            self.widgets[w].SetValue('')
          except: pass
      matchFile.write(json.dumps(info))
    self.matchNumberSelection.SetValue(int(self.matchNumberSelection.GetValue())+1)
  def OnMatchNoSelect(self, e):
    global currentMatchNo
    currentMatchNo=e.GetInt()
  def OnRobotStationSelect(self, e):
    global currentSuffix
    s = e.GetString()
    currentSuffix=s[0].lower()+s[4]

app = wx.App()
Client(None, title="FRC Field Scouting")

app.MainLoop()