
Private Sub btnOK_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnOK.Click
        Dim EnteredKey As String
        EnteredKey = UCase(txtActKey1.Text)
        'Remove all hyphens
        Dim P As Integer
        P = Strings.InStr(EnteredKey, "-")
        While P > 0
            If P > 1 Then
                EnteredKey = Strings.Left(EnteredKey, P - 1) & Strings.Right(EnteredKey, Strings.Len(EnteredKey) - P)
            Else
                EnteredKey = Strings.Right(EnteredKey, Strings.Len(EnteredKey) - 1)
            End If
            P = Strings.InStr(EnteredKey, "-")
        End While
        'Now check for valid key
        msLicense = ValidateActivationKey(EnteredKey)
       If msLicense = "" Then
            Dim Resp As Long
            Resp = MsgBox("The key entered is not a valid activation key." & _
                   "  Do you wish to activate in Demo mode?", MsgBoxStyle.YesNo, _
                   "BioCommand Activation")
            If Resp = vbYes Then
                msLicense = "Demo"
            Else
                Me.DialogResult = Windows.Forms.DialogResult.None
                txtActKey1.Focus()
                Exit Sub
            End If
        End If
        Me.DialogResult = System.Windows.Forms.DialogResult.OK
        Me.Close()
    End Sub
    Private Function ValidateActivationKey(ByVal EnteredKey As String) As String
        Dim License As String
        'Create an instance of the key calculator
        Dim KeyCalc As New clsActivator()
        Dim MsgStr1 As String
        Dim MsgStr2 As String
        MsgStr1 = "The serial number entered is for a version different from the one selected." & vbCrLf
        MsgStr1 = MsgStr1 & "A license has been activated for "
        MsgStr2 = "  If this is not correct please contact NBS."
        'Test for matches
        If CleanActivationKey(EnteredKey) = CleanActivationKey(KeyCalc.ActKeyFromRegKey(msRegKey, "Platinum", "M1326-0020", msSerNo)) Then
            License = "Platinum"
        ElseIf CleanActivationKey(EnteredKey) = CleanActivationKey(KeyCalc.ActKeyFromRegKey(msRegKey, "Gold", "M1326-0010", msSerNo)) Then
            License = "Gold"
            If msProdNum = "M1326-0020" Then
                MsgBox(MsgStr1 & "BioCommand Batch Control." & MsgStr2, MsgBoxStyle.OkOnly, "BioCommand Activation")
            End If
        ElseIf CleanActivationKey(EnteredKey) = CleanActivationKey(KeyCalc.ActKeyFromRegKey(msRegKey, "Silver", "M1326-0000", msSerNo)) Then
            License = "Silver"
            If msProdNum = "M1326-0010" Or msProdNum = "M1326-0020" Then
                MsgBox(MsgStr1 & "BioCommand Track and Trend." & MsgStr2, MsgBoxStyle.OkOnly, "BioCommand Activation")
            End If
            'ElseIf EnteredKey = KeyCalc.ActKeyFromRegKey(msRegKey, "Demo", msProdNum, msSerNo) Then
            '    License = "Demo"
        Else
            License = ""
        End If
        Return License
    End Function
    Private Function CleanActivationKey(ByVal InKey As String) As String
        'This function scans the input key replacing any zeros with 'O' and any ones with 'I'
        Dim OutStr As String = ""
        Dim I As Integer
        For I = 1 To Strings.Len(InKey)
            If Strings.Mid(InKey, I, 1) = "0" Then
                OutStr = OutStr & "O"
            ElseIf Strings.Mid(InKey, I, 1) = "1" Then
                OutStr = OutStr & "I"
            Else
                OutStr = OutStr & Strings.Mid(InKey, I, 1)
            End If
        Next
        Return OutStr
    End Function
