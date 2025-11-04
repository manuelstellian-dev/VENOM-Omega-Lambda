package com.venom.aios.main

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private val TAG = "MainActivity"
    private lateinit var organism: VenomOrganism
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        Log.i(TAG, "VENOM MainActivity starting...")
        
        organism = VenomOrganism.getInstance(this)
        
        setContent {
            VenomTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    VenomScreen(organism)
                }
            }
        }
    }
    
    override fun onDestroy() {
        organism.shutdown()
        super.onDestroy()
    }
}

@Composable
fun VenomScreen(organism: VenomOrganism) {
    val scope = rememberCoroutineScope()
    var vitals by remember { mutableStateOf(organism.getVitals()) }
    var isInitialized by remember { mutableStateOf(false) }
    var messages by remember { mutableStateOf(listOf<ChatMessage>()) }
    var currentInput by remember { mutableStateOf("") }
    
    // Initialize organism
    LaunchedEffect(Unit) {
        val success = organism.birth()
        if (success) {
            isInitialized = true
            organism.startVitalsMonitoring { newVitals ->
                vitals = newVitals
            }
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Title
        Text(
            text = "VENOM Ω-Λ Organism",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Vitals Card
        VitalsCard(vitals = vitals, isInitialized = isInitialized)
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Chat Interface
        ChatInterface(
            messages = messages,
            currentInput = currentInput,
            onInputChange = { currentInput = it },
            onSend = {
                if (currentInput.isNotBlank()) {
                    val userMessage = ChatMessage(currentInput, true)
                    messages = messages + userMessage
                    
                    val query = currentInput
                    currentInput = ""
                    
                    scope.launch {
                        val response = organism.interact(query)
                        val botMessage = ChatMessage(response, false)
                        messages = messages + botMessage
                    }
                }
            },
            enabled = isInitialized,
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
fun VitalsCard(vitals: OrganismVitals, isInitialized: Boolean) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "System Vitals",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                VitalItem("θ", String.format("%.3f", vitals.theta))
                VitalItem("Λ", String.format("%.0f", vitals.lambdaScore))
                VitalItem("Nodes", vitals.meshNodes.toString())
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                VitalItem("CPU", String.format("%.0f%%", vitals.cpuHealth * 100))
                VitalItem("MEM", String.format("%.0f%%", vitals.memoryUsage * 100))
                VitalItem("Battery", "${vitals.batteryLevel}%")
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = if (isInitialized && vitals.isAlive) "STATUS: ALIVE" else "STATUS: INITIALIZING",
                style = MaterialTheme.typography.bodyMedium,
                color = if (vitals.isAlive) Color(0xFF4CAF50) else Color(0xFFFFC107),
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun VitalItem(label: String, value: String) {
    Column {
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyLarge,
            fontWeight = FontWeight.Medium
        )
    }
}

data class ChatMessage(val text: String, val isUser: Boolean)

@Composable
fun ChatInterface(
    messages: List<ChatMessage>,
    currentInput: String,
    onInputChange: (String) -> Unit,
    onSend: () -> Unit,
    enabled: Boolean,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        // Messages
        val listState = rememberLazyListState()
        
        LaunchedEffect(messages.size) {
            if (messages.isNotEmpty()) {
                listState.animateScrollToItem(messages.size - 1)
            }
        }
        
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            contentPadding = PaddingValues(vertical = 8.dp)
        ) {
            items(messages) { message ->
                ChatBubble(message)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
        
        // Input
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = currentInput,
                onValueChange = onInputChange,
                modifier = Modifier.weight(1f),
                placeholder = { Text("Talk to VENOM…") },
                enabled = enabled
            )
            
            Spacer(modifier = Modifier.width(8.dp))
            
            IconButton(
                onClick = onSend,
                enabled = enabled && currentInput.isNotBlank()
            ) {
                Icon(Icons.Default.Send, "Send")
            }
        }
    }
}

@Composable
fun ChatBubble(message: ChatMessage) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (message.isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            shape = RoundedCornerShape(12.dp),
            color = if (message.isUser) 
                MaterialTheme.colorScheme.primary 
            else 
                MaterialTheme.colorScheme.surfaceVariant,
            modifier = Modifier.widthIn(max = 280.dp)
        ) {
            Text(
                text = message.text,
                modifier = Modifier.padding(12.dp),
                color = if (message.isUser) 
                    MaterialTheme.colorScheme.onPrimary 
                else 
                    MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
